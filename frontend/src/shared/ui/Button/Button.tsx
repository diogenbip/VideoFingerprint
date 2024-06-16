"use client"

import React from "react"
import cx from "classnames"
import { Loader } from "../Loader/Loader"

interface IButton {
  title: string
  disabled?: boolean
  loading?: boolean
  variant?: "primary" | "secondary"
  onClick?: () => void
}

export const Button: React.FC<IButton> = ({title, disabled = false , loading = false, variant = "primary", onClick}) => {
  return (
      <button
        disabled={disabled}
        className={cx(`min-w-36 h-10 border rounded-md inline-flex items-center justify-center py-3 px-7 text-center text-base font-medium   disabled:bg-gray-200 disabled:text-gray-400 disabled:border-gray-200 transition`,
          variant === "primary" ? "bg-black border-black text-white hover:bg-white hover:text-black" : "bg-white border-black text-black hover:bg-black hover:text-white hover:border-white",
          {
            "pointer-events-none": loading
          }
        )}
        onClick={onClick}
      >
        {loading ? (
          <Loader size="small"/>
        ) : title}
      </button>
  )
}