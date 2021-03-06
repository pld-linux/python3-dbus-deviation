#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%if %{without python3}
%undefine	with_doc
%endif
Summary:	Parse D-Bus introspection XML and process it in varous ways
Summary(pl.UTF-8):	Analiza opisów XML protokołu D-Bus i przetwarzanie na różne sposoby
Name:		python-dbus-deviation
Version:	0.6.0
Release:	2
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dbus-deviation/
Source0:	https://files.pythonhosted.org/packages/source/d/dbus-deviation/dbus-deviation-%{version}.tar.gz
# Source0-md5:	0b0bdee54cb82dcc5641f977527a9daf
URL:		https://pypi.org/project/dbus-deviation/
%if %{with python2}
BuildRequires:	python-Sphinx
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_git >= 0.3
BuildRequires:	python-setuptools_pep8
%if %{with tests}
BuildRequires:	python-lxml
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_git >= 0.3
BuildRequires:	python3-setuptools_pep8
%if %{with tests}
BuildRequires:	python3-lxml
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dbus-deviation is a project for parsing D-Bus introspection XML and
processing it in various ways. Its main tool is dbus-interface-diff,
which calculates the difference between two D-Bus APIs for the purpose
of checking for API breaks.

This functionality is also available as a Python module,
dbusdeviation.

%description -l pl.UTF-8
dbus-deviation to projekt do analizy opisów XML protokołu D-Bus i
przetwarzania ich na różne sposoby. Główne narzędzie to
dbus-interface-diff, wyliczające różnice między dwoma API D-Bus na
potrzeby sprawdzania zmian API.

Funkcjonalność jest dostępna także jako moduł Pythona dbusdeviation.

%package -n python3-dbus-deviation
Summary:	Parse D-Bus introspection XML and process it in varous ways
Summary(pl.UTF-8):	Analiza opisów XML protokołu D-Bus i przetwarzanie na różne sposoby
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-dbus-deviation
dbus-deviation is a project for parsing D-Bus introspection XML and
processing it in various ways. Its main tool is dbus-interface-diff,
which calculates the difference between two D-Bus APIs for the purpose
of checking for API breaks.

This functionality is also available as a Python module,
dbusdeviation.

%description -n python3-dbus-deviation -l pl.UTF-8
dbus-deviation to projekt do analizy opisów XML protokołu D-Bus i
przetwarzania ich na różne sposoby. Główne narzędzie to
dbus-interface-diff, wyliczające różnice między dwoma API D-Bus na
potrzeby sprawdzania zmian API.

Funkcjonalność jest dostępna także jako moduł Pythona dbusdeviation.

%package apidocs
Summary:	API documentation for Python dbus-deviation module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dbus-deviation
Group:		Documentation

%description apidocs
API documentation for Python dbus-deviation module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dbus-deviation.

%prep
%setup -q -n dbus-deviation-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test} %{?with_doc:build_sphinx}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/{dbusapi,dbusdeviation}/tests
%py_postclean

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/dbus-interface-*
%endif
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/{dbusapi,dbusdeviation}/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%if %{without python3}
%attr(755,root,root) %{_bindir}/dbus-interface-diff
%attr(755,root,root) %{_bindir}/dbus-interface-vcs-helper
%endif
%{py_sitescriptdir}/dbusapi
%{py_sitescriptdir}/dbusdeviation
%{py_sitescriptdir}/dbus_deviation-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-dbus-deviation
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/dbus-interface-diff
%attr(755,root,root) %{_bindir}/dbus-interface-vcs-helper
%{py3_sitescriptdir}/dbusapi
%{py3_sitescriptdir}/dbusdeviation
%{py3_sitescriptdir}/dbus_deviation-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build-3/sphinx/html/{_modules,_static,*.html,*.js}
%endif
