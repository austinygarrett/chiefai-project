import { Avatar, Group, Menu, Text, UnstyledButton } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import cx from 'clsx';
import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useLogout, useUser } from '@/lib/auth';
import { User } from '@/types/api';
import './topbar.scss';

import logo from '@/assets/images/chiefai-logo-inverse.png';
import { useCalendarUpload } from '@/features/dashboard/api/upload-calendar';

export const TopBar = () => {
  const logout = useLogout();
  const user = useUser().data as User;
  const navigate = useNavigate();
  const [userMenuOpened, setUserMenuOpened] = useState(false);
  const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] =
    useDisclosure(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const { mutate: uploadCalendar, isPending, isSuccess } = useCalendarUpload();
  const handleUploadClick = () => {
    inputRef.current?.click(); // Open file dialog
  };
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    uploadCalendar({
      data: {
        calendarFile: file,
        source: 'Google Calendar',
        tags: ['work', 'team'],
      },
    });
  };

  return (
    <div className={cx('header', !user && 'unauthenticated')}>
      <div className="mainSection">
        <Group className="top-bar-main-section" justify={'space-between'}>
          <img src={logo} alt="ChiefAI Logo" className="logo" />
          {user && user.email && (
            <Group>
              <Menu
                width={260}
                position="bottom-end"
                transitionProps={{ transition: 'pop-top-right' }}
                onClose={() => setUserMenuOpened(false)}
                onOpen={() => setUserMenuOpened(true)}
                withinPortal
              >
                <Menu.Target>
                  <UnstyledButton
                    className={cx('user', userMenuOpened && 'userActive')}
                  >
                    <Group gap={16}>
                      <Group className="profile-summary">
                        <Text fw={500} size="sm" lh={1} mr={3}>
                          {user.email}
                        </Text>
                      </Group>
                      <Avatar
                        className="avatar"
                        alt={user.email}
                        radius="xl"
                        size={35}
                      >
                        {user.email.charAt(0).toUpperCase()}
                      </Avatar>
                    </Group>
                  </UnstyledButton>
                </Menu.Target>
                <input
                  type="file"
                  ref={inputRef}
                  accept=".ics"
                  onChange={handleFileChange}
                  style={{ display: 'none' }}
                />
                <Menu.Dropdown>
                  <Menu.Item onClick={handleUploadClick}>
                    Upload Calendar
                  </Menu.Item>
                  <Menu.Item
                    onClick={() => {
                      const body = document.body;
                      body.classList.remove('login-screen', 'app-screen');
                      logout.mutate({});
                    }}
                    color="red"
                  >
                    Log out
                  </Menu.Item>
                </Menu.Dropdown>
              </Menu>
            </Group>
          )}
        </Group>
      </div>
    </div>
  );
};
