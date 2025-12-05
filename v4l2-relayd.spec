%global commit d6ec36aae87e765eddef8308f0f58c7b5be95ad7
%global commitdate 20251028
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           v4l2-relayd
Summary:        Utils for relaying the video stream between two video devices
Version:        0.2.0
Release:        1.%{commitdate}git%{shortcommit}%{?dist}
License:        GPL-2.0-only

Source0:        https://gitlab.com/vicamo/v4l2-relayd//-/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        v4l2-relayd.preset

BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glib2-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  systemd

Requires:       v4l2loopback

%description
This is used to relay the input GStreamer source to an output GStreamer
source or a V4L2 device.

%prep
%autosetup -p1 -n %{name}-%{commit}
autoreconf --force --install --verbose

%build
%configure
%make_build

%install
%make_install modprobedir=%{_modprobedir}
sed -i '/^EnvironmentFile=\/etc\/default\/v4l2-relayd/a EnvironmentFile=-\/run\/v4l2-relayd' %{buildroot}%{_unitdir}/v4l2-relayd.service
sed -i 's/Virtual Camera/Intel MIPI Camera/g' %{buildroot}%{_modprobedir}/v4l2-relayd.conf
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_presetdir}/95-v4l2-relayd.preset
ln -s /run/v4l2-relayd  %{buildroot}%{_sysconfdir}/v4l2-relayd.d/icamerasrc.conf

%post
%systemd_post v4l2-relayd.service

%preun
%systemd_preun v4l2-relayd.service

%postun
%systemd_postun_with_restart v4l2-relayd.service

%files
%license LICENSE
%{_bindir}/v4l2-relayd
%{_sysconfdir}/default/v4l2-relayd
%dir %{_sysconfdir}/v4l2-relayd.d
%{_sysconfdir}/v4l2-relayd.d/icamerasrc.conf
%{_modprobedir}/v4l2-relayd.conf
%{_modulesloaddir}/v4l2-relayd.conf
%{_systemdgeneratordir}/v4l2-relayd-generator
%{_unitdir}/v4l2-relayd.service
%{_unitdir}/v4l2-relayd@.service
%{_presetdir}/95-v4l2-relayd.preset

%changelog
* Fri Dec 05 2025 Kate Hsuan <hpa@redhat.com> - 0.2.0-1.20251028gitd6ec36a
- Update to upstream release 0.2.0

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.2-15.20220126git2e4d5c9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.2-14.20220126git2e4d5c9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.2-13.20220126git2e4d5c9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.2-12.20220126git2e4d5c9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.2-11.20220126git2e4d5c9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 3 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-10.20220126git2e4d5c9
- Set output stream to I420

* Fri Apr 7 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-9.20220126git2e4d5c9
- Removed unnecessary install command

* Thu Mar 23 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-8.20220126git2e4d5c9
- Drop the symbolic link of the environment file
- Add EnvironmentFile setting for /run/v4l2-relayd

* Wed Mar 22 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-7.20220126git2e4d5c9
- systemd post scripts
- removed configuration examples

* Mon Mar 20 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-6.20220126git2e4d5c9
- remove udev rules

* Tue Mar 14 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-5.20220126git2e4d5c9
- Configuration files for Tiger and Alder lake platforms
- udev rules for config file selection

* Tue Feb 21 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-4.20220126git2e4d5c9
- New private event ID

* Thu Feb 16 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-3.20220126git2e4d5c9
- Update build and installation scripts

* Thu Jan 12 2023 Kate Hsuan <hpa@redhat.com> - 0.1.2-2.20220126git2e4d5c9
- Add "Requires: v4l2loopback"

* Thu Dec 15 2022 Kate Hsuan <hpa@redhat.com> - 0.1.2-1.20220126git2e4d5c9
- First commit

