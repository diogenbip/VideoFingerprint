"use client"

import { useState } from "react";
import { Button } from "../Button/Button";

export const Header = () => {

  const [open, setOpen] = useState(false);

  return (
    <header className="flex w-full items-center justify-between bg-black text-white p-6">
      <div>Debug dream team</div>
      {/* <div className="grid grid-cols-2 gap-3">
        <Button variant="secondary" title="User" />
        <Button variant="secondary" title="Moderator" />
      </div> */}
    </header>
  )
}

