"use client";
import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [input, setInput] = useState("");
  const [out, setOut] = useState("");

  const submit = async () => {
    const r = await axios.post("http://localhost:8000/design", { question: input });
    setOut(r.data.answer);
  };

  return (
    <main className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">System Design Assistant</h1>
      <textarea value={input} onChange={e=>setInput(e.target.value)} className="w-full border p-2" rows={5}/>
      <button onClick={submit} className="bg-blue-600 text-white px-4 py-2 rounded mt-2">Generate</button>
      <div className="prose mt-6"><ReactMarkdown>{out}</ReactMarkdown></div>
    </main>
  );
}
