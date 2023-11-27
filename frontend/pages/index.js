'use client'

import Head from 'next/head';
import styles from '../styles/Poll.module.css';
import { useState, useEffect } from 'react';

const HALF_PAGE_SCALE_FACTOR = 50;

const getBarHeight = (score, totalVotes) => {
  if (totalVotes === 0) return 0;
  return `${(Math.abs(score) / totalVotes) * HALF_PAGE_SCALE_FACTOR}%`
}

const POSITIVE_COLOR = "bg-green-500";
const NEGATIVE_COLOR = "bg-red-500";

const POSITIVE_TRANSLATE = "-translate-y-1/2";
const NEGATIVE_TRANSLATE = "translate-y-1/2";

export default function Poll() {
  const initialVoteSummary = {
    score: 0,
    total_votes: 0,
    positive_votes: 0,
    negative_votes: 0,
  };

  const [voteSummary, setVoteSummary] = useState(initialVoteSummary);
  const [opacity, setOpacity] = useState("opacity-0")
  const [translate, setTranslate] = useState(POSITIVE_TRANSLATE);
  const [color, setColor] = useState(POSITIVE_COLOR);

  fetch("https://api.brad.coffee/vote_summary")
    .then(response => response.json())
    .then(newSummary => {
      setVoteSummary(newSummary)
    })
    .catch(error => console.log(error))

  const updateBarStyles = (newVoteSummary) => {
    if (newVoteSummary.score > 0) {
      setColor(POSITIVE_COLOR)
      setTranslate(POSITIVE_TRANSLATE)
      setOpacity("");
    }
    if (newVoteSummary.score < 0) {
      setColor(NEGATIVE_COLOR)
      setTranslate(NEGATIVE_TRANSLATE)
      setOpacity("");
    }
    if (newVoteSummary.score === 0) {
      setOpacity("opacity-0");
    }
  }

  useEffect(() => {
    const voteSummarySource = new EventSource("https://api.brad.coffee/stream");
    voteSummarySource.addEventListener("summary", (event) => {
      const newVoteSummary = JSON.parse(event.data)
      setVoteSummary(newVoteSummary)
      updateBarStyles(newVoteSummary)
    });

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
        ${styles["transition-bar"]} ease-in-out duration-500
        ${opacity} ${translate} ${color}
        `} style={{ height: getBarHeight(voteSummary.score, voteSummary.total_votes) }}>
      </div>
    </div >
  );
}
