import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="card">
      <h1 className="text-4xl font-bold mb-4">Welcome to the AI Email Generator</h1>
      <p className="mb-6 text-center max-w-lg">
        Use AI to craft professional emails from summary points instantly.
      </p>
      <Link to="/email">
        <button className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
          Get Started
        </button>
      </Link>
    </div>
  );
}
