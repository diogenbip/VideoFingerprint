import { create } from "zustand";

interface IDownloadStore {
  file: File | null
  updateFile: (file: File| null) => void
}

export const useDownloadStore = create<IDownloadStore>((set) => ({
  file: null,
  updateFile: (file: File | null) => set({ file }),
}))