import { useState, useEffect } from "react";
import { Router, Route, Switch } from "wouter";
import ChessPuzzle from "./components/ChessPuzzle";

function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Use the current host for API calls in Replit environment
    const apiUrl = window.location.origin + "/api/hello";
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => setMessage(data.message))
      .catch((error) => {
        console.error("Error:", error);
        setMessage("Failed to fetch message from server");
      });
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="max-w-lg w-full bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">
          Chess Mate Puzzle
        </h1>
        <p className="text-gray-600 mb-4">
          {message || "Loading message from backend..."}
        </p>

        <div className="mt-4">
          <ChessPuzzle />
        </div>
      </div>
    </div>
  );
}

function PuzzleDetail({ params }: { params: { id: string } }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="max-w-lg w-full bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">
          Chess Puzzle #{params.id}
        </h1>

        <div className="mt-4">
          <ChessPuzzle puzzleId={params.id} />
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/puzzle/:id" component={PuzzleDetail} />
        <Route>404 - Not Found</Route>
      </Switch>
    </Router>
  );
}
