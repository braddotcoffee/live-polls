import React from "react"
import PropTypes from "prop-types"

const getThresholdIndicatorPlacement = (threshold) => {
  return `bottom-[${threshold}%]`
}

export default function SuccessThresholdIndicator(props) {
  return (
    <div
      className={`
        w-12 h-2
        absolute left-0 ${getThresholdIndicatorPlacement(props.threshold)}
        ${props.color}
      `}
    ></div>
  )
}

SuccessThresholdIndicator.propTypes = {
  threshold: PropTypes.number,
  color: PropTypes.string,
}
