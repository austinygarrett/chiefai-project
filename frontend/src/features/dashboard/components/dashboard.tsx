import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import { DeepChat } from 'deep-chat-react';

import './dashboard.scss';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import MDEditor from '@uiw/react-md-editor';
import { useUser } from '@/lib/auth';
import { Paper, Stack } from '@mantine/core';
import { User } from '@/types/api';
import { useEffect, useRef, useState } from 'react';
import { useCalendarEvents } from '../api/get-calendar-events';

const localizer = momentLocalizer(moment);

export const DashboardComponent = () => {
  const user = useUser().data as User;
  const [history, setHistory] = useState<any[]>([]);
  const [briefingBookText, setBriefingBookText] = useState('');

  const { refetch, data: events, isLoading, error } = useCalendarEvents();
  const chatRef = useRef<any>(null);
  const messageStyles = {
    default: {
      shared: {
        bubble: {
          maxWidth: '95%',
          width: '100%',
          marginTop: '10px',
        },
      },
    },
    loading: {
      message: {
        styles: {
          bubble: {
            width: '1em',
          },
        },
      },
    },
  };

  const htmlClassUtilities = {
    'add-to-briefing-book-btn': {
      styles: {
        default: {
          marginTop: '8px',
          padding: '6px 12px',
          fontSize: '14px',
          borderRadius: '6px',
          backgroundColor: '#1971c2',
          color: 'white',
          cursor: 'pointer',
          border: 'none',
          textAlign: 'center',
        },
        hover: {
          backgroundColor: '#1864ab',
        },
      },
      events: {
        click: () => {
          console.log('click');
          const messages = chatRef.current?.getMessages?.();
          const lastAssistantMsg = messages?.at(-1)?.text;

          if (lastAssistantMsg) {
            setBriefingBookText((prev) =>
              prev ? `${prev}\n\n${lastAssistantMsg}` : lastAssistantMsg,
            );
          }
        },
      },
    },
  };

  if (isLoading) return <p>Loading events...</p>;
  if (error) return <p>Error: {error.message}</p>;

  const calendarEvents = events?.map((event) => ({
    title: event.summary,
    start: new Date(event.start_time),
    end: new Date(event.end_time),
    allDay: false, // optional, based on your data
    resource: event, // store original if needed
  }));

  return (
    <div className="dashboard-component-container">
      <Paper className="calendar-container" shadow="xs" p="md" withBorder>
        <h2>Calendar</h2>

        <Stack flex={1}>
          <Calendar
            defaultView="day"
            localizer={localizer}
            events={calendarEvents}
            startAccessor="start"
            endAccessor="end"
            views={['day']}
          />
        </Stack>
      </Paper>
      <Paper className="briefing-book-container" shadow="xs" p="md" withBorder>
        <Stack className="briefing-book-content">
          <h2>Briefing book</h2>
          <div className="briefing-book" data-color-mode="light">
            <MDEditor
              autoFocus={true}
              value={briefingBookText}
              autoFocusEnd={true}
              visibleDragbar={false}
              onChange={(val) => setBriefingBookText(val || '')}
              height={'100%'}
            />
          </div>
        </Stack>
      </Paper>
      <Paper className="ask-ai-container" shadow="xs" p="md" withBorder>
        <Stack className="ask-ai-content">
          <h2>Ask ChiefAI</h2>
          <DeepChat
            ref={chatRef}
            connect={{
              url: 'http://localhost:8080/api/v1/calendar/chat',
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              credentials: 'include',
            }}
            style={{ borderRadius: '4px', width: '100%', height: '100%' }}
            textInput={{ placeholder: { text: 'Ask ChiefAI a question!' } }}
            history={history}
            messageStyles={messageStyles}
            htmlClassUtilities={htmlClassUtilities}
          />
        </Stack>
      </Paper>
    </div>
  );
};
