%define lua_version %(lua -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define lua_archdir %{_libdir}/lua/%{lua_version}
%global lua_libdir %{_libdir}/lua/%{lua_version}

Name:           lua-mpack
Version:        1.0.4
Release:        2
Summary:        Implementation of MessagePack for Lua 5.1
License:        MIT
Group:          Development/Other
Url:            https://github.com/tarruda/libmpack
Source:         https://github.com/tarruda/libmpack/archive/%{version}.tar.gz
BuildRequires:  libtool
BuildRequires:  lua-devel
Requires:       lua

%description

mpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

%prep
%setup -q -n libmpack-%{version}

# hack to export flags
pushd binding/lua
echo '#!/bin/sh' > ./configure
chmod +x ./configure
popd

%build
pushd binding/lua
%configure
%make %{?_smp_mflags} \
     USE_SYSTEM_LUA=yes \
     LUA_VERSION_MAJ_MIN=%{lua_version} \
     LUA_LIB=$(pkg-config --libs lua)
popd

%install
pushd binding/lua
%make USE_SYSTEM_LUA=yes \
     LUA_CMOD_INSTALLDIR=%{lua_libdir} \
     DESTDIR=%{buildroot} \
     install
popd

%files
%doc LICENSE-MIT README.md
%dir %{lua_archdir}
%{lua_archdir}/*
