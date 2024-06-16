"use client"

import { useEffect, useState } from "react";
import cx from "classnames"
import { NotificationStatus, useToastStore } from "../stores/toastStore";

const STEP = 90;

export interface IToastNotification {
  children: React.ReactNode
}

interface IToast {
  status: NotificationStatus;
  message: string;
  offset?: number;
  removeToast: () => void;
}

const INITIAL_BOTTOM = 50;

export const Toast: React.FC<IToast> = ({
  status,
  message,
  offset = 0,
  removeToast,
}: IToast) => {
  const [isRemoved, setIsRemoved] = useState<boolean>(false);

  const handleRemove = () => {
    setIsRemoved(true);
    setTimeout(() => {
      removeToast();
    }, 100)
  };

  useEffect(() => {
    const timerId = setTimeout(() => {
      handleRemove();
    }, 4000 + offset);

    return () => {
      clearTimeout(timerId);
    };
  }, []);

  return (
    <div 
      className={cx("flex justify-between items-center py-2.5 px-5 w-auto h-auto min-h-[60px] fixed left-1/2 transition-all duration-300 ease-out rounded-xl text-sm z-[99999] bg-white shadow-md", {
        "border-2 border-green-500": status === 'success',
        "border-2 border-red-500": status === 'danger',
      })}
      style={{
        bottom: `${INITIAL_BOTTOM + offset}px`,
        transform: `translateX(-50%) ${isRemoved ? 'scale(0)' : ''}`,
      }}
    >
      <div className={"flex items-center gap-2.5"}>
        <p className={"m-0 p-0"}>{message}</p>
      </div>
      <button 
        className={"ml-[15px] cursor-pointer"}
        onClick={handleRemove}
      >
        X
      </button>
    </div>
  )
}

export const ToastNotificationProvider: React.FC<IToastNotification> = ({
  children,
}) => {
  const { notifications, removeNotification } = useToastStore();

  return (
    <>
      {children}
      <div>
        {notifications.map((notification, index) => (
          <Toast
            key={`toast-notif-${notification.id}`}
            status={notification.status}
            message={notification.message}
            offset={index * STEP}
            removeToast={() => removeNotification(notification.id)}
          />
        ))}
      </div>
    </>
  );
}

export const useToast = () => {
  const { addNotification } = useToastStore();

  return {
    error: (message: string) => addNotification("danger", message),
    success: (message: string) => addNotification("success", message),
    info: (message: string) => addNotification("info", message),
    warning: (message: string) => addNotification("warning", message),
  };
};