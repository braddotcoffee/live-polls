'use client'

import Head from 'next/head';
import styles from '../styles/Poll.module.css';
import { useState, useEffect } from 'react';


export default function Poll() {
  let initialVoteSummary = {
    score: 0,
    total_votes: 0,
  };

  const [voteSummary, setVoteSummary] = useState(initialVoteSummary);

  fetch("https://api.brad.coffee/vote_summary")
    .then(response => response.json())
    .then(newSummary => setVoteSummary(newSummary))
    .catch(error => console.log(error))

  useEffect(() => {
    console.log("Running use effect")
    const voteSummarySource = new EventSource("https://api.brad.coffee/stream");
    voteSummarySource.addEventListener("summary", (event) => setVoteSummary(JSON.parse(event.data)));

    return () => {
      voteSummarySource.close();
    }
  }, [])

  return (
    <div className={styles.container}>
      <Head>
        <script src="https://cdn.tailwindcss.com"></script>
      </Head>
      <h1 className="text-7xl text-slate-700">Test 123</h1>
      <div>
        Score: {voteSummary.score}
      </div>
      <div>
        Total Votes: {voteSummary.total_votes}
      </div>
    </div>
  );
}
