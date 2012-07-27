#
# spec file for package UIEsearching (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:           UIEsearching
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Accessible information searching tool for UI Automation
Provides:	UIEsearching
Obsoletes:	UIEsearching
Version:        0.1
Release:        2
Source0:        %name-%version.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Accessible information searching tool for UI Automation test

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools/%name
cp -a * $RPM_BUILD_ROOT/usr/share/qa/tools/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/qa/tools

%changelog
* Thu Jul 26 2012 - cachen@suse.com
- Create the second version: add pygtk UI app
* Thu Sep 29 2011 - cachen@suse.com
- Create the first version
