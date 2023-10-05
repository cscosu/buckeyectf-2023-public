import { signIn, signOut, useSession } from "next-auth/react";
import { useState } from "react";
import { toast } from "react-hot-toast";

import Head from "next/head";
import Image from "next/image";
import { AiFillGithub } from "react-icons/ai";
import { GoRepo } from "react-icons/go";
import { HiOutlinePaperAirplane } from "react-icons/hi";
import { MdLogout } from "react-icons/md";

import { api } from "~/utils/api";
import { env } from "~/env.mjs";

const Home = () => {
  return (
    <>
      <Head>
        <title>Smederij</title>
        <meta name="description" content="Smederij GitHub CTF challenge" />
        <link rel="icon" href="/smederij.svg" />
      </Head>
      <main className="flex flex-auto justify-center sm:mt-20">
        <Card />
      </main>
    </>
  );
};

export default Home;

const Card = () => {
  return (
    <div className="bg-gray-300 p-4 sm:max-w-xl sm:rounded-xl">
      <div className="flex items-center gap-2">
        <Image src="/smederij.svg" alt="Smederij" width={75} height={75} />
        <div>
          <h1 className="text-4xl">Smederij</h1>
        </div>
      </div>

      <div className="m-4">
        <div className="mb-4 flex flex-col gap-2">
          <div>
            This is a CTF challenge involving GitHub. This website is{" "}
            <b>not in scope</b>, and is used only for automation in setting up
            the challenge. If you encounter any issues, contact{" "}
            <span className="font-mono">mbund</span> in the BuckeyeCTF Discord.
            A GitHub account is required.
          </div>
          <div>
            Once you auth with your GitHub account below, you will be invited to
            a private repository created for you under the{" "}
            <span className="font-mono">smederij</span> organization (it may
            take a minute). You can then also optionally invite additional team
            members to your repository, or they can create their own.
          </div>
          <div>Laat het smeden beginnen!</div>
        </div>
        <LowerCard />
      </div>
    </div>
  );
};

const LowerCard = () => {
  const { status } = useSession();

  if (status == "loading") return <></>;

  if (status == "authenticated") return <AuthedInterface />;

  return (
    <div className="flex justify-center">
      <button
        className="rounded bg-gray-300 p-2 font-bold text-gray-800 hover:bg-gray-400"
        onClick={() => void signIn("github")}
      >
        <AiFillGithub fontSize={35} className="mr-2 inline" />
        <span className="align-middle">Auth with GitHub</span>
      </button>
    </div>
  );
};

const AuthedInterface = () => {
  const { data: sessionData } = useSession();

  const repoInfo = api.github.repoInfo.useQuery();
  const createRepo = api.github.createRepo.useMutation({
    onSuccess: (repo) => {
      toast.success(`Created repo ${repo}`, {
        duration: 5000,
      });
      void repoInfo.refetch();
    },
    onError: (data) => toast.error(data.message),
  });

  if (repoInfo.data === undefined) return <>Loading...</>;
  if (!sessionData) return <>Something went wrong</>;

  return (
    <div>
      <div>
        {repoInfo.data?.numberOfInvites > 0 ? (
          <div>
            {repoInfo.data.repositoryName && (
              <div className="mb-4 p-2">
                <a
                  href={`https://github.com/smederij/${repoInfo.data.repositoryName}`}
                >
                  <GoRepo className="mr-1 inline" fontSize={25} />
                  <span>smederij/{repoInfo.data.repositoryName}</span>
                </a>
              </div>
            )}
            <div>{repoInfo.data.numberOfInvites}/4 players</div>
            <InviteBox />
          </div>
        ) : (
          <button
            className="inline-flex items-center rounded bg-gray-300 p-2 font-bold text-gray-800 enabled:hover:bg-gray-400 disabled:text-gray-400"
            onClick={() => createRepo.mutate()}
            disabled={createRepo.isLoading || repoInfo.data.createdRepos > 0}
          >
            <GoRepo className="mr-2" fontSize={25} />
            <span>Create Challenge Repository</span>
          </button>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between">
        <div>
          <a href={`https://github.com/${sessionData.user.login}`}>
            <img
              src={sessionData.user.image}
              className="mr-2 inline rounded-full"
              width={32}
              height={32}
              alt={`${sessionData.user.login}'s profile image`}
            />
            <span className="align-middle">
              {sessionData.user?.name && (
                <>
                  <b>{sessionData.user?.name}</b> aka{" "}
                </>
              )}
              <b>{sessionData.user?.login}</b>
            </span>
          </a>
        </div>
        <button
          className="rounded bg-gray-300 p-2 font-bold text-gray-800 hover:bg-gray-400"
          onClick={() => void signOut()}
        >
          <span className="mr-2 align-middle">Sign Out</span>
          <MdLogout className="inline" fontSize={25} />
        </button>
      </div>
    </div>
  );
};

const InviteBox = () => {
  const [username, setUsername] = useState("");
  const repoInfo = api.github.repoInfo.useQuery();
  const inviteUser = api.github.inviteUser.useMutation({
    onSuccess: (user) => {
      toast.success(`Invited user ${user}`, { duration: 5000 });
      void repoInfo.refetch();
      setUsername("");
    },
    onError: (e) => {
      const errorMessage = e.data?.zodError?.fieldErrors.username;
      if (errorMessage && errorMessage[0]) {
        toast.error(errorMessage[0]);
      } else {
        toast.error(e.message);
      }
    },
  });

  return (
    <div className="relative">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          inviteUser.mutate({ username });
        }}
      >
        <input
          className="w-full appearance-none rounded border-2 border-gray-200 bg-gray-200 px-4 py-2 pr-10 leading-tight text-gray-700 focus:border-gray-500 focus:bg-gray-100 focus:outline-none"
          type="text"
          placeholder="GitHub username..."
          value={username}
          disabled={inviteUser.isLoading}
          onChange={(e) => setUsername(e.target.value)}
          minLength={1}
        ></input>
        <button className="absolute right-2 h-full rotate-90" type="submit">
          <HiOutlinePaperAirplane fontSize={25} />
        </button>
      </form>
    </div>
  );
};
