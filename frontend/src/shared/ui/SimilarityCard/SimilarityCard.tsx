"use client"

import { useEffect, useRef, useState } from "react"
import cx from "classnames"
import { Loader } from "../Loader/Loader"
import axios from "../../lib/axios"

interface ISimilarityCard {
  video1Url?: string,
  video2Url?: string,
  similarity?: {
    s1: number,
    e1: number,
    s2: number,
    e2: number
  }
}

export const SimilarityCard: React.FC<ISimilarityCard> = ({video1Url, video2Url, similarity}) => {
  const video1Ref = useRef(null);
  const timeline1Ref = useRef(null)
  const [thumbnails, setThumbnails] = useState<string[] | null>(null)

  const leftValue = 2

  useEffect(() => {
    const fetchVideoData = async () => {
      try {
        const filename = '0ac7ed0507b2364e40030d11bf52ee5d.mp4'; // Замените на актуальное имя файла
        const response = await axios.get(`/getThumbnails/${filename}`);
        setThumbnails(response.data);
        console.log(response.data)
      } catch (error) {
        console.log('ERROR')
      }
    };

    fetchVideoData();
  }, []);

  return (
    <div className=" w-1/3 relative border border-dashed rounded-md min-h-[175px] p-6 flex flex-col items-center justify-center">
      {video1Url && video2Url && similarity ? (
        <>
        <div className="text-2xl py-4">Coincidences</div>
        <div className="pb-4 text-center">Your video matches this video in the segment from your video from {similarity.s1} second to {similarity.e1} seconds. A piece from this video from {similarity.e1} seconds to {similarity.e2} seconds</div>
        <div className="flex flex-col items-center">
          <div className="relative w-full flex flex-col">
            <video 
              ref={video1Ref}
              src={video1Url}
              controls
            />
            {/* Thumbnails */}
             {/* <div className="flex relative items-center h-[120px] mt-10 w-full overflow-hidden" ref={timeline1Ref}>
              {thumbnails && thumbnails.map((filename, index) => (
                <div
                className="flex-thumbnail"
                  key={index}
                >
                  <img
                    src={`http://127.0.0.1:5000/${filename}`}
                    className={`object-cover h-[100px] cursor-pointer opacity-[0.7] transition-opacity delay-200 ease-in-out`}
                  />
                </div>
              ))}
              {similarity && (
                <div className={cx(`absolute top-[10px] w-[40px] h-[100px] bg-red-500 opacity-50 border-l border-r border-red-500`, `left-[${leftValue}%]`)}
                />
              )}
            </div> */}
          </div>
        </div>
        </>
      ) : (
      <div className="flex flex-col items-center justify-center">
        <div className="mb-4">
          Processing video ...
        </div>
        <Loader size="large"/>
      </div>
    )}
    </div>
  )
}