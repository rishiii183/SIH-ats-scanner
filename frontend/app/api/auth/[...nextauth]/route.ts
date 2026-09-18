import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { supabase } from "@/lib/supabase";

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
        name: { label: "Name", type: "text" },
        mode: { label: "Mode", type: "text" },
      },
      async authorize(credentials) {
        if (!credentials?.email) {
          throw new Error("Please enter your email address.");
        }

        const email = credentials.email.toLowerCase().trim();
        const mode = credentials.mode || "login";
        const name = credentials.name?.trim() || email.split("@")[0];

        // 1. Check if user already exists in Supabase
        const { data: existingUser, error: fetchError } = await supabase
          .from("users")
          .select("*")
          .eq("email", email)
          .maybeSingle();

        if (mode === "login") {
          // --- LOGIN LOGIC ---
          if (!existingUser) {
            throw new Error("No account found with this email. Please sign up first.");
          }

          return {
            id: existingUser.id,
            name: existingUser.name || name,
            email: existingUser.email,
          };
        } else {
          // --- SIGNUP LOGIC ---
          if (existingUser) {
            throw new Error("An account with this email already exists. Please log in.");
          }

          const { data: newUser, error: insertError } = await supabase
            .from("users")
            .insert({
              email,
              name,
              auth_provider: "email",
            })
            .select()
            .single();

          if (insertError) {
            console.error("Supabase signup error:", insertError);
            throw new Error(insertError.message || "Failed to create account.");
          }

          return {
            id: newUser.id,
            name: newUser.name,
            email: newUser.email,
          };
        }
      },
    }),
  ],
  session: {
    strategy: "jwt",
  },
  secret: process.env.NEXTAUTH_SECRET,
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async signIn({ user, account }) {
      if (user?.email && account?.provider === "google") {
        try {
          const { error } = await supabase.from("users").upsert(
            {
              email: user.email.toLowerCase().trim(),
              name: user.name || "",
              auth_provider: "google",
            },
            { onConflict: "email" }
          );
          if (error) {
            console.error("Supabase Google user sync error:", error);
          }
        } catch (err) {
          console.error("Exception syncing user to Supabase:", err);
        }
      }
      return true;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.name = token.name || session.user.name;
        session.user.email = token.email || session.user.email;
      }
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
  },
});

export { handler as GET, handler as POST };
