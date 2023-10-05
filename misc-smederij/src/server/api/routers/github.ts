import { Octokit } from "octokit";
import sodium from "libsodium-wrappers";
import { globby } from "globby";
import { readFile } from "fs/promises";
import crypto from "node:crypto";
import path from "path";
import { z } from "zod";

import { createTRPCRouter, protectedProcedure } from "~/server/api/trpc";
import { env } from "~/env.mjs";
import { TRPCError } from "@trpc/server";

const ORGANIZATION = "smederij";

const octo = new Octokit({
  auth: env.GITHUB_PERSONAL_ACESSS_TOKEN,
});

export const githubRouter = createTRPCRouter({
  repoInfo: protectedProcedure.query(async ({ ctx }) => {
    const user = await ctx.prisma.user.findUnique({
      where: { id: ctx.session.user.id },
    });

    if (!user)
      throw new TRPCError({
        code: "INTERNAL_SERVER_ERROR",
        message: "User not found",
      });

    return {
      createdRepos: user.createdRepos,
      repositoryName: user.repositoryName,
      numberOfInvites: user.numberOfInvites,
    };
  }),

  inviteUser: protectedProcedure
    .input(
      z.object({
        username: z
          .string()
          .min(1, "Invited username must be at least one character"),
      })
    )
    .mutation(async ({ input, ctx }) => {
      const user = await ctx.prisma.user.findUnique({
        where: { id: ctx.session.user.id },
      });

      if (!user)
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: "You were not found",
        });
      if (user.createdRepos <= 0)
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: "You must have created a repo",
        });
      if (!user.repositoryName)
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: "You must have created a repo",
        });
      if (user.numberOfInvites >= 4)
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: "You cannot invite more than 4 collaborators",
        });

      const githubUser = await octo.rest.users
        .getByUsername({
          username: input.username,
        })
        .catch(() => {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: `Could not find invitee user ${input.username}`,
          });
        });

      await octo.rest.repos
        .addCollaborator({
          owner: ORGANIZATION,
          repo: user.repositoryName,
          username: input.username,
          permission: "pull",
        })
        .catch(() => {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: "Could not invite user to repo",
          });
        });

      // invite to organization
      // await octo.rest.orgs
      //   .createInvitation({
      //     org: ORGANIZATION,
      //     invitee_id: githubUser.data.id,
      //   })
      //   .catch(() => {
      //     console.log(
      //       `Could not invite ${ctx.session.user.login} to org (user could already be in it)`
      //     );
      //   });

      await ctx.prisma.user.update({
        where: { id: ctx.session.user.id },
        data: { numberOfInvites: { increment: 1 } },
      });

      return input.username;
    }),

  createRepo: protectedProcedure.mutation(async ({ ctx }) => {
    // use the db as a mutex to only allow the user to create a repo once
    const user = await ctx.prisma.user.update({
      where: { id: ctx.session.user.id },
      data: { createdRepos: { increment: 1 } },
    });

    if (user.createdRepos > 1)
      throw new TRPCError({
        code: "INTERNAL_SERVER_ERROR",
        message: "You can only create one repo",
      });

    const REPO = "smith-" + crypto.randomBytes(8).toString("hex");

    console.log(
      `Creating repo ${ORGANIZATION}/${REPO} for user ${ctx.session.user.login}`
    );

    try {
      const createRepo = await octo.rest.repos.createInOrg({
        org: ORGANIZATION,
        name: REPO,
        auto_init: true,
        private: true,
      });

      type RepsonseHeaders = typeof createRepo.headers;

      const debugRatelimits = (scope: string, headers: RepsonseHeaders) => {
        const limit = headers["x-ratelimit-limit"];
        const remaining = headers["x-ratelimit-remaining"];
        const reset = headers["x-ratelimit-reset"];

        if (!limit || !remaining || !reset) return;

        console.log(
          `${scope} ratelimit ${remaining}/${limit} requests resets at ${reset}`
        );
      };

      debugRatelimits("Create repo", createRepo.headers);

      await uploadToRepo(
        octo,
        "./template",
        ORGANIZATION,
        REPO,
        "Begin smithing :hammer:"
      );

      const public_key = await octo.rest.actions.getRepoPublicKey({
        owner: ORGANIZATION,
        repo: REPO,
      });

      const secret = env.FLAG;
      const key = public_key.data.key;

      const encrypted_secret = await sodium.ready.then(() => {
        const binkey = sodium.from_base64(key, sodium.base64_variants.ORIGINAL);
        const binsec = sodium.from_string(secret);
        const encBytes = sodium.crypto_box_seal(binsec, binkey);
        return sodium.to_base64(encBytes, sodium.base64_variants.ORIGINAL);
      });

      await octo.rest.actions.createOrUpdateRepoSecret({
        owner: ORGANIZATION,
        repo: REPO,
        secret_name: "FLAG",
        encrypted_value: encrypted_secret,
        key_id: public_key.data.key_id,
      });

      const addCollaborator = await octo.rest.repos.addCollaborator({
        owner: ORGANIZATION,
        repo: REPO,
        username: ctx.session.user.login,
        permission: "pull",
      });

      debugRatelimits("Add collaborator", addCollaborator.headers);

      const githubUser = await octo.rest.users.getByUsername({
        username: ctx.session.user.login,
      });

      await octo.rest.orgs
        .createInvitation({
          org: ORGANIZATION,
          invitee_id: githubUser.data.id,
        })
        .catch(() => {
          console.log(
            `Could not invite ${ctx.session.user.login} to org (user could already be in it)`
          );
        });

      await ctx.prisma.user.update({
        where: { id: ctx.session.user.id },
        data: { numberOfInvites: { increment: 1 }, repositoryName: REPO },
      });

      console.log(
        `Created repo ${ORGANIZATION}/${REPO} for user ${ctx.session.user.login}`
      );

      return `${ORGANIZATION}/${REPO}`;
    } catch (error) {
      await ctx.prisma.user.update({
        where: { id: ctx.session.user.id },
        data: { createdRepos: { set: 0 } },
      });

      throw error;
    }
  }),
});

const uploadToRepo = async (
  octo: Octokit,
  coursePath: string,
  owner: string,
  repo: string,
  commitMessage: string,
  branch = "main"
) => {
  const filePaths = await globby(coursePath, { dot: true, gitignore: true });
  const fileBlobs = await Promise.all(
    filePaths.map(createBlobForFile(octo, owner, repo))
  );

  const blobPaths = filePaths.map((fullPath) =>
    path.relative(coursePath, fullPath)
  );

  const newTree = await createNewTree(octo, owner, repo, fileBlobs, blobPaths);

  const newCommit = await octo.rest.git.createCommit({
    owner,
    repo,
    message: commitMessage,
    tree: newTree.sha,
  });

  await octo.rest.git.updateRef({
    owner,
    repo,
    ref: `heads/${branch}`,
    sha: newCommit.data.sha,
    force: true,
  });
};

const getFileAsBase64 = (filePath: string) =>
  readFile(filePath, { encoding: "base64" });

const createBlobForFile =
  (octo: Octokit, owner: string, repo: string) => async (filePath: string) => {
    const content = await getFileAsBase64(filePath);
    const blobData = await octo.rest.git.createBlob({
      owner,
      repo,
      content,
      encoding: "base64",
    });
    return blobData.data;
  };

const createNewTree = async (
  octo: Octokit,
  owner: string,
  repo: string,
  blobs: {
    url: string;
    sha: string;
  }[],
  paths: string[]
) => {
  const tree = blobs.map(({ sha }, index) => ({
    path: paths[index],
    mode: "100644",
    type: "blob",
    sha,
  })) as {
    path: string;
    mode: "100644";
    type: "blob";
    sha: string;
  }[];

  const { data } = await octo.rest.git.createTree({
    owner,
    repo,
    tree,
  });
  return data;
};
