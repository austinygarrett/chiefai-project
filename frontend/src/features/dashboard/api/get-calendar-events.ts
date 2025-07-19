import { z } from 'zod';

import { api } from '@/lib/api-client';
import {
  useQuery,
  UseQueryOptions,
  UseQueryResult,
} from '@tanstack/react-query';

export const calendarEventSchema = z.object({
  id: z.number().optional(),
  event_uid: z.string(),
  user_id: z.number(),
  status: z.string(),
  summary: z.string(),
  start_time: z.string().datetime(),
  end_time: z.string().datetime(),
  rrule: z.string().nullable(),
  exdates: z.array(z.string().datetime()).nullable(),
  dtstamp: z.string().datetime().nullable(),
  event_created: z.string().datetime().nullable(),
  last_modified: z.string().datetime().nullable(),
  sequence: z.number().nullable(),
  transp: z.string().nullable(),
  embedding: z.array(z.number()).nullable(),
  created_at: z.string().datetime().nullable(),
  updated_at: z.string().datetime().nullable(),
  deleted_at: z.string().datetime().nullable(),
});

export const calendarEventsSchema = z.array(calendarEventSchema);

export type CalendarEvent = z.infer<typeof calendarEventSchema>;

export const getCalendarEvents = async (): Promise<CalendarEvent[]> => {
  const response = await api.get('/calendar/');
  return calendarEventsSchema.parse(response.data);
};

export const useCalendarEvents = (
  options?: UseQueryOptions<CalendarEvent[], Error>,
): UseQueryResult<CalendarEvent[], Error> => {
  return useQuery({
    queryKey: ['calendar-events'],
    queryFn: getCalendarEvents,
    ...options,
  });
};
