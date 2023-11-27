'use client'

import Head from 'next/head';
import styles from '../styles/Poll.module.css';
import { useState, useEffect } from 'react';

const HALF_PAGE_SCALE_FACTOR = 50;

const getBarHeight = (score, totalVotes) => {
  return `${(Math.abs(score) / totalVotes) * HALF_PAGE_SCALE_FACTOR}%`
}

export default function Poll() {
  let initialVoteSummary = {
    score: 0,
    total_votes: 0,
    positive_votes: 0,
    negative_votes: 0,
  };

  const [voteSummary, setVoteSummary] = useState(initialVoteSummary);


  fetch("https://api.brad.coffee/vote_summary")
    .then(response => response.json())
    .then(newSummary => setVoteSummary(newSummary))
    .catch(error => console.log(error))

  useEffect(() => {
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
      <div id="bar" className={`
        w-12 absolute left-0
        transition-all ease-in-out duration-500
        ${voteSummary.score > 0 ? "-translate-y-1/2 bg-green-500" : "translate-y-1/2 bg-red-500"}
        ${voteSummary.score == 0 ? "opacity-0" : ""}
        `} style={{ height: getBarHeight(voteSummary.score, voteSummary.total_votes) }}>

      </div>
    </div >
  );
}
