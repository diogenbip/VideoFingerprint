"use client"

import { useEffect, useState } from "react";
import { useDownloadStore } from "../src/shared/stores/downloadStore";
import { Button } from "../src/shared/ui/Button/Button";
import { DragNDrop } from "../src/shared/ui/DragNDrop/DragNDrop";
import axios from "../src/shared/lib/axios";
import { useToast } from "../src/shared/hooks/useToast";
import { SimilarityCard } from "../src/shared/ui/SimilarityCard/SimilarityCard";
import Confetti from "../src/shared/ui/Confetti/Confetti";


export default function Home() {

  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [isMatchesGet, setIsMathcesGet] = useState(false)
  const [showConfetti, setShowConfetti] = useState(false)
  const [matches, setMatches] = useState<[{videoUrl: string, similarity: {s1: number, e1: number, s2: number, e2: number}}]>()

  const file = useDownloadStore(state => state.file)
  const toast = useToast()

  const handleUpload = async () => {

    if(!file) return

    const formData = new FormData();
    formData.append('video', file)

    try {
      setIsUploading(true)
      setUploadProgress(0)
      const respone = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded / (progressEvent.total ?? 1)) * 100)
          setUploadProgress(progress)
          if (progress === 100) {
            setIsUploading(false)
          }
        },

      })
      console.log('File uploaded successfully', respone.data)
      toast.success('Video uploaded successfully')
      //TODO: Вызвать процессинг
      setIsMathcesGet(true)
      setShowConfetti(true);
      setTimeout(() => {
        setShowConfetti(false);
      }, 3000);
    } catch (error) {
      setIsUploading(false)
      console.error('Error uploading file', error)
      toast.error('Oops... Something went wrong. Please try again later.')
      setIsMathcesGet(true)
      setShowConfetti(true);
      setTimeout(() => {
        setShowConfetti(false);
      }, 3000);
    }
  }

  return (
    <main className="flex flex-col items-center justify-center p-24">
      <div className="flex flex-col items-center w-full">
        <div className="xl:w-1/3">
          <DragNDrop />
        </div>
        <div className="my-10">
          <Button disabled={!file || uploadProgress === 100} loading={isUploading || (uploadProgress === 100 && !isMatchesGet)} title="Upload" onClick={handleUpload}/>
        </div>
      </div>
      <div className="w-full flex flex-col items-center">
        {matches?.map((el, index) => (
        <SimilarityCard 
          key={index}
          video1Url={el.videoUrl}
          video2Url={el.videoUrl}
          similarity={el.similarity}
        />
      ))}
      </div>
      <div className="w-full flex flex-col items-center">
        {isMatchesGet && (
          <>
          <div className="flex flex-col items-center justify-center xl:w-1/3 border border-dashed rounded-md min-h-[175px] p-6">
            <div className="flex flex-col gap-2 my-10 text-center">
              <div>
            К сожалению наше решение не может найти совпадения, но вы можете посмотреть как мы реализовали алгоритм фингерпринта и сохранения его в бд на нашем гитхаб 😊
              </div>
              <div>
            А еще в презентации мы сделали анализ рынка и конкурентов, так что тоже обязательно посмотрите 😊
              </div>
              
              </div>

              <div className="flex flex-col md:flex-row justify-around items-center w-full">
                <div className=" my-10  flex justify-around">
                  <Button title="GitHub" onClick={() => window.open('https://github.com/diogenbip/VideoFingerprint/', '_blank')}/>
                </div>
                <div className=" my-10 flex justify-around">
                  <Button title="Презентация" onClick={() => window.open('https://disk.yandex.ru/d/Lr8zHCDRzhgQ9g', '_blank')}/>
                </div>
              </div>
          </div>
          </>
        )}
      </div>
      {showConfetti && <Confetti />}
    </main>
  );
}
