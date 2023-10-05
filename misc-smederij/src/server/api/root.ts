import { createTRPCRouter } from "~/server/api/trpc";
import { githubRouter } from "~/server/api/routers/github";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
  github: githubRouter,
});

// export type definition of API
export type AppRouter = typeof appRouter;
