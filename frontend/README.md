# Frontend placeholder

The frontend will be implemented with **Next.js** (TypeScript), **Tailwind CSS**, and **NextAuth** for authentication.  
For the initial commit we only provide a placeholder.  Future iterations will scaffold the Next.js application with pages for:

1. Google sign‑in via NextAuth.  
2. Uploading Netflix CSV files.  
3. Connecting your YouTube account.  
4. Viewing recommendations and explanations.  
5. Visualizing the knowledge graph using Cytoscape.js.

Once scaffolded, you can run the frontend with:

```sh
cd frontend
npm install
npm run dev
```

To configure OAuth and API endpoints, copy `.env.example` to `.env.local` and fill in the appropriate values.  The frontend will read configuration from environment variables prefixed with `NEXT_PUBLIC_`.
