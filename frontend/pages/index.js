'use client'

import Script from 'next/script';
import Head from 'next/head';
import styles from '../styles/Poll.module.css';
import { useState, useEffect } from 'react';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;
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
    //not sure why score and total_votes are stored, since they can be derived from positive_votes and negative_votes.
    score: 0,
    total_votes: 0,
    positive_votes: 0,
    negative_votes: 0,
  };

  const [voteSummary, setVoteSummary] = useState(initialVoteSummary);
  const [opacity, setOpacity] = useState("opacity-0")
  const [translate, setTranslate] = useState(POSITIVE_TRANSLATE);
  const [color, setColor] = useState(POSITIVE_COLOR);

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
    fetch(`${BASE_URL}/vote_summary`)
      .then(response => response.json())
      .then(newSummary => {
        setVoteSummary(newSummary)
        updateBarStyles(newSummary)
      })
      .catch(error => console.log(error))

    const voteSummarySource = new EventSource(`${BASE_URL}/stream`);
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
    <>
      <Script src="https://cdn.tailwindcss.com" />
      //not sure why styles.container is used instead of tailwind, the following tailwind styles can replace it
      //min-h-[100vh] p-[0 0.5rem] w-12 flex flex-col justify-center items-center
      <div className={styles.container}>
        <Head>
          <title>Poll Overlay</title>
        </Head>
        <div id="bar" className={`
        w-12 absolute left-0
        ${styles["transition-bar"]} ease-in-out duration-500
        ${opacity} ${translate} ${color}
        `} style={{ height: getBarHeight(voteSummary.score, voteSummary.total_votes) }}>
        </div>

        <div className={`
        absolute left-[12px] font-semibold mb-[80px]
        ease-in-out duration-500 
         ${translate}
        `} style={{ height: getBarHeight(voteSummary.score, voteSummary.total_votes) }}>
          <p className='font-semibold text-4xl text-green-500 '>{voteSummary.positive_votes}</p>
        </div>
        
        <div className={`
        absolute left-[12px] flex flex-col justify-end mt-[80px] 
        ease-in-out duration-500 
         ${translate}
        `} style={{ height: getBarHeight(voteSummary.score, voteSummary.total_votes) }}>
          <p className='font-semibold text-4xl text-red-500 '>{voteSummary.negative_votes}</p>
        </div>

      </div >
    </>
  );
}
