AutoReqProv: no

##Init variables

%global packver 83
%global _optdir /opt
%ifarch x86_64
%global arch linux64
%else
%global arch linux
%endif

##Package Version and Licences

Summary: Firefox Nightly RPM Builds
Name: firefox-nightly
Version: %{packver}
Release: 0a1_%(date +%%y%%m%%d)%{?dist}
License: MPLv1.1 or GPLv2+ or LGPLv2+
Source0: https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=%{arch}#/%{name}-%{version}.tar.gz
Source1: firefox-nightly.desktop
Source2: default-policies.json
Group: Applications/Internet
URL: http://www.nightly.mozilla.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: alsa-lib libX11 libXcomposite libXdamage libnotify libXt libXext glib2 dbus-glib libjpeg-turbo cairo-gobject libffi fontconfig freetype libgcc gtk3 gtk2 hunspell zlib
Requires: nspr >= 4.10.8
Requires: nss >= 3.19.2
Requires: sqlite >= 3.8.10.2

##Description for Package

%description
This package is a package built directly from Mozilla's nightly tarball. This package will be updated weekly if not sooner.

%prep
%setup -q -n firefox

## Install Instructions

%install

## Firefox explicitly supports python3, so its also our choice of interpreter. Note that there is no dependency on python.
## These scripts are only used when generating debug information in case of a crash, so not critical to the operation of firefox.
find %{_builddir} -name '*.py' -type f -exec sed -i -e 's,#!/usr/bin/python,#!/usr/bin/python3,' -e 's,/usr/bin/env python,/usr/bin/env python3,' -s {} \;

install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/128x128/apps},opt}
install -dm 755 %{buildroot}/%{_optdir}/firefox-nightly/browser/defaults/preferences/

install -m644 %{_builddir}/firefox/browser/chrome/icons/default/default128.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/firefox-nightly.png

cp -rf %{_builddir}/firefox/* %{buildroot}/opt/firefox-nightly/
ln -s /opt/firefox-nightly/firefox %{buildroot}/usr/bin/firefox-nightly

%{__cp} -p %{SOURCE1} %{buildroot}/%{_datadir}/applications/%{name}.desktop

## Disable Update Alert
%{__mkdir_p} %{buildroot}/%{_optdir}/firefox-nightly/distribution
%{__cp} -p %{SOURCE1} %{buildroot}/%{_optdir}/firefox-nightly/distribution/policies.json

##Cleanup

%clean
rm -rf $RPM_BUILD_ROOT

##Installed Files


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_optdir}/firefox-nightly/
