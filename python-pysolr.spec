# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global srcname pysolr


Name:           python-pysolr
Version:        3.3.0
Release:        1%{?dist}
Summary:        A lightweight Python wrapper for Apache Solr

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-requests
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif


Requires:  python-requests
%if 0%{?with_python3}
Requires:  python3-requests
%endif


%description
pysolr is a lightweight Python wrapper for Apache Solr. It provides an interface
that queries the server and returns results based on the query.


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        A lightweight Python wrapper for Apache Solr

%description -n python3-%{srcname}
pysolr is a lightweight Python wrapper for Apache Solr. It provides an interface
that queries the server and returns results based on the query.
%endif


%prep
%setup -q -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{srcname}.*
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%endif


%changelog
* Sat Mar  7 2015 Joe Tsoi <joe.yeung.tsoi@gmail.com> 3.3.0-1
- Initial package.
