#
# tohkbd2-daemon spec
# (C) kimmoli 2014
#

Name:       harbour-tohkbd2

%{!?qtc_qmake:%define qtc_qmake %qmake}
%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}
%{?qtc_builddir:%define _builddir %qtc_builddir}

Summary:    The OtherHalf Keyboard version 2 daemon
Version:    0.0.devel
Release:    1
Group:      Qt/Qt
License:    LICENSE
URL:        https://github.com/kimmoli/tohkbd2-daemon
Source0:    %{name}-%{version}.tar.bz2

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(mlite5)

Requires:   ambienced
Requires:   harbour-tohkbd2user

%description
Daemon for The OtherHalf Keyboard (TOHKBD) version 2

%prep
%setup -q -n %{name}-%{version}

%build

%qtc_qmake5 SPECVERSION=%{version}

%qtc_make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%qmake5_install

%files
%defattr(644,root,root,755)
%attr(6711,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}
%config /etc/systemd/user
%config /etc/udev/rules.d
%config /etc/dbus-1/system.d
%config /usr/share/maliit/plugins/com/jolla/layouts
%{_datadir}/ambience/%{name}

%post
#reload udev rules
udevadm control --reload
# if tohkbd2 is connected, start daemon now
# vendor id 6537 = 0x1989 = dirkvl
# product id 3 = tohkbd2
if [ -e /sys/devices/platform/toh-core.0/vendor ]; then
 if grep -q 6537 /sys/devices/platform/toh-core.0/vendor ; then
  if grep -q 3 /sys/devices/platform/toh-core.0/product ; then
   systemctl-user start %{name}.service
  fi
 fi
fi
%_ambience_post

%pre
# In case of update, stop and disable first
if [ "$1" = "2" ]; then
  systemctl-user stop %{name}.service
  systemctl-user disable %{name}.service
  udevadm control --reload
fi

%preun
# in case of complete removal, stop and disable
if [ "$1" = "0" ]; then
  systemctl-user stop %{name}.service
  systemctl-user disable %{name}.service
  udevadm control --reload
fi
