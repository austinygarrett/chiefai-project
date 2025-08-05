import { default as dayjs } from 'dayjs';

export const formatDate = (date: Date) => dayjs(date).format('MM/DD/YY');
export const formatDateDetailed = (date: Date) =>
  dayjs(date).format('MM/DD/YY hh:mm:ss a');
