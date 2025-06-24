import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"; // <-- Import useNavigate

export default function EmailApp() {
  const [summary, setSummary] = useState("");
  const [recipientEmail, setRecipientEmail] = useState("");
  const navigate = useNavigate(); // <-- Hook for navigation

  const handleGenerate = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          summary,
          email: recipientEmail
        })
      });

      const data = await res.json();

      if (data.success) {
        // Navigate to email view with email data
        navigate("/generated-email", { state: { email: data } });
      } else {
        alert("Failed to generate email: " + data.error);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Backend error occurred. See console for details.");
    }
  };

  return (
    <>
      <div className="card1">
        <Link to="/" className="text-blue-600 underline mb-6 block">← Back to Home</Link>
        <h2 className="text-2xl font-semibold mb-4">Generate Email from Summary</h2>

        <form onSubmit={handleGenerate} className="flex flex-col gap-4 max-w-xl">
          <input
            type="email"
            placeholder="Recipient Email"
            value={recipientEmail}
            onChange={(e) => setRecipientEmail(e.target.value)}
            className="border border-gray-300 rounded-lg p-3"
            required
          />

          <textarea
            rows={6}
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            placeholder="Enter summary points here..."
            className="border border-gray-300 rounded-lg p-3"
            required
          />
          <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
            Generate Email
          </button>
        </form>
      </div>
    </>
  );
}
