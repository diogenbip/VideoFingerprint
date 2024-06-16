import { create } from "zustand";
import { uuidv4 } from "../utils/utils";

export type NotificationStatus = "success" | "danger" | "warning" | "info";

interface Notification {
  message: string;
  status: NotificationStatus;
  id: string;
}

interface ToastState {
  notifications: Notification[];
  addNotification: (status: NotificationStatus, message: string) => void;
  removeNotification: (id: string) => void;
}

export const useToastStore = create<ToastState>((set) => ({
  notifications: [],
  addNotification: (status, message) =>
    set((state) => {
      const newNotification = { id: uuidv4(), status, message };
      const updatedNotifications = [...state.notifications, newNotification];
      return {
        notifications: updatedNotifications.slice(-5),
      };
    }),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter(
        (notification) => notification.id !== id
      ),
    })),
}));
