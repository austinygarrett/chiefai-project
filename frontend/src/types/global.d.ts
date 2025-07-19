export {};

declare global {
  interface Window {
    chatRef: any;
    briefingBookRef: HTMLTextAreaElement | null;
    addToBriefingBook: () => void;
  }
}
