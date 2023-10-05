Bun.serve({
  port: 5000,
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/") return new Response(Bun.file("solve.html"));
    if (url.pathname === "/wait") {
      await new Promise((r) => setTimeout(r, 5 * 1000));
      return new Response(`404!`, { status: 404 });
    }
    if (url.pathname === "/flag") {
      console.log(req.url);
      return new Response(`Hello`);
    }
    return new Response(`None`, { status: 404 });
  },
});
