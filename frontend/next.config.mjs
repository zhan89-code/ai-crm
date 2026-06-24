/** @type {import("next").NextConfig} */
const config = {
  output: "standalone",
  async rewrites() {
    return [{ source: "/api/:path*", destination: "http://api:8000/api/:path*" }]
  },
}
export default config