"use client"

import React, { useState, useEffect } from "react"
import Script from "next/script"
import Head from "next/head"
import styles from "../styles/Poll.module.css"
import SuccessThresholdIndicator from "../components/successThresholdIndicator"

const BASE_URL = process.env.NEXT_PUBLIC_API_URL
const SUCCESS_THRESHOLD = process.env.NEXT_PUBLIC_SUCCESS_THRESHOLD
const HALF_PAGE_SCALE_FACTOR = 50

const getBarHeight = (score, totalVotes) => {
  if (totalVotes === 0) return 0
  return `${(Math.abs(score) / totalVotes) * HALF_PAGE_SCALE_FACTOR}%`
}

const showSuccessThreshold = (voteSummary) =>
  SUCCESS_THRESHOLD !== undefined && voteSummary.total_votes > 0

const getPositiveRatio = (voteSummary) =>
  Math.floor((voteSummary.positive_votes / voteSummary.total_votes) * 100)

const POSITIVE_COLOR = "bg-green-500"
const NEGATIVE_COLOR = "bg-red-500"
const SUCCESS_COLOR = "bg-pink-300"

const POSITIVE_TRANSLATE = "-translate-y-1/2"
const NEGATIVE_TRANSLATE = "translate-y-1/2"

export default function Poll() {
  const initialVoteSummary = {
    score: 0,
    total_votes: 0,
    positive_votes: 0,
    negative_votes: 0,
  }

  const [voteSummary, setVoteSummary] = useState(initialVoteSummary)
  const [opacity, setOpacity] = useState("opacity-0")
  const [translate, setTranslate] = useState(POSITIVE_TRANSLATE)
  const [color, setColor] = useState(POSITIVE_COLOR)

  const updateBarStyles = (newVoteSummary) => {
    if (newVoteSummary.score > 0) {
      if (
        SUCCESS_THRESHOLD !== undefined &&
        getPositiveRatio(newVoteSummary) >= SUCCESS_THRESHOLD
      ) {
        setColor(SUCCESS_COLOR)
      } else {
        setColor(POSITIVE_COLOR)
      }
      setTranslate(POSITIVE_TRANSLATE)
      setOpacity("")
    }
    if (newVoteSummary.score < 0) {
      setColor(NEGATIVE_COLOR)
      setTranslate(NEGATIVE_TRANSLATE)
      setOpacity("")
    }
    if (newVoteSummary.score === 0) {
      setOpacity("opacity-0")
    }
  }

  useEffect(() => {
    fetch(`${BASE_URL}/vote_summary`)
      .then((response) => response.json())
      .then((newSummary) => {
        setVoteSummary(newSummary)
        updateBarStyles(newSummary)
      })

    const voteSummarySource = new EventSource(`${BASE_URL}/stream`)
    voteSummarySource.addEventListener("summary", (event) => {
      const newVoteSummary = JSON.parse(event.data)
      setVoteSummary(newVoteSummary)
      updateBarStyles(newVoteSummary)
    })

    return () => {
      voteSummarySource.close()
    }
  }, [])

  return (
    <>
      <Script src="https://cdn.tailwindcss.com" />
      <Head>
        <title>Poll Overlay</title>
      </Head>
      <div
        className="
          min-h-[100vh] p-[0 0.5rem]
          w-12 flex flex-col
          justify-center items-center"
      >
        <div
          id="bar"
          className={`
            w-12 absolute left-0
            ${styles["transition-bar"]} ease-in-out duration-500
            ${opacity} ${translate} ${color}
          `}
          style={{
            height: getBarHeight(voteSummary.score, voteSummary.total_votes),
          }}
        />
      </div>
      <div
        className={`
        transition-opacity ease-in-out duration-500
        ${showSuccessThreshold(voteSummary) ? "opacity-100" : "opacity-0"}
        `}
      >
        {showSuccessThreshold(voteSummary) && (
          <SuccessThresholdIndicator
            threshold={SUCCESS_THRESHOLD}
            color={SUCCESS_COLOR}
          />
        )}
      </div>
    </>
  )
}
