import {
  useMutation,
  UseMutationOptions,
  UseMutationResult,
  useQueryClient,
} from '@tanstack/react-query';
import { z } from 'zod';
import { api } from '@/lib/api-client';

// Optional metadata schema
const calendarMetadataSchema = z.object({
  source: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

export type CalendarUploadInput = z.infer<typeof calendarMetadataSchema> & {
  calendarFile: File;
};

type CalendarUploadInputVariables = {
  data: CalendarUploadInput;
};

export const uploadCalendar = async ({
  data,
}: CalendarUploadInputVariables): Promise<any> => {
  const formData = new FormData();
  formData.append('calendarFile', data.calendarFile);

  // Add optional metadata
  const { calendarFile, ...metadata } = data;
  formData.append(
    'metadata',
    new Blob([JSON.stringify(metadata)], { type: 'application/json' }),
  );

  const response = await api.put(`/calendar/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const useCalendarUpload = (
  options?: UseMutationOptions<any, Error, CalendarUploadInputVariables>,
): UseMutationResult<any, Error, CalendarUploadInputVariables> => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: uploadCalendar,
    onSuccess: (data, variables, context) => {
      // Invalidate calendar events so DashboardComponent refetches them
      queryClient.invalidateQueries({ queryKey: ['calendar-events'] });

      // Call user-defined onSuccess if any
      options?.onSuccess?.(data, variables, context);
    },
    ...options,
  });
};
