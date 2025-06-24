import { useLocation, Link, useNavigation, useNavigate } from "react-router-dom";

export default function GeneratedEmail() {
  const location = useLocation();
  const email = location.state?.email;
  const nav = useNavigate();

  if (!email) {
    return (
      <div className="card">
        <p>No email data found. Please generate one first.</p>
        <Link to="/email" className="text-blue-500 underline">Generate Email</Link>
      </div>
    );
  }

  return (
    <div className="card">
      <Link to="/">← Back to Home</Link>
      <h2>Generated Email</h2>
      <p><strong>Subject:</strong> {email.subject}</p>
      <p><strong>Body:</strong><br />{email.body}</p>
      <button onClick={()=>nav("/email")}>Generate Again</button>
    </div>
  );
}
