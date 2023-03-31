%define lua_version %(lua -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define lua_archdir %{_libdir}/lua/%{lua_version}
%global lua_libdir %{_libdir}/lua/%{lua_version}

%define luajit_version %(luajit -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define luajit_archdir %{_libdir}/lua/%{luajit_version}
%global luajit_libdir %{_libdir}/lua/%{luajit_version}

Name:           lua-mpack
Version:        1.0.9
Release:        2
Summary:        Implementation of MessagePack for Lua
License:        MIT
Group:          Development/Other
Url:            https://github.com/libmpack/libmpack-lua
Source:         https://github.com/libmpack/libmpack-lua/archive/refs/tags/%{version}.tar.gz
Source1:	https://github.com/tarruda/libmpack/archive/1.0.5.tar.gz
BuildRequires:  libtool
BuildRequires:  lua-devel
Requires:       lua
BuildRequires:	luajit
BuildRequires:	pkgconfig(luajit)

%description
mpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

%package -n luajit-mpack
Summary:        Implementation of MessagePack for LuaJIT

%description -n luajit-mpack
mpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

%prep
%autosetup -p1 -n libmpack-lua-%{version}

%build
%make_build %{?_smp_mflags} \
	USE_SYSTEM_LUA=yes \
	CFLAGS="%{optflags}" \
	LUA_VERSION_MAJ_MIN=%{lua_version} \
	LUA_LIB=$(pkg-config --libs lua) \
	FETCH=cat \
	MPACK_URL="%{S:1}"
mv mpack.so mpack.so.lua
%make_build clean

%make_build %{?_smp_mflags} \
	USE_SYSTEM_LUA=yes \
	CFLAGS="%{optflags}" \
	LUA_VERSION_MAJ_MIN=%{luajit_version} \
	LUA_IMPL=luajit \
	LUA_LIB=$(pkg-config --libs luajit) \
	FETCH=cat \
	MPACK_URL="%{S:1}"


%install
%make_install \
	USE_SYSTEM_LUA=yes \
	LUA_CMOD_INSTALLDIR=%{luajit_libdir} \
	LUA_VERSION_MAJ_MIN=%{luajit_version} \
	LUA_IMPL=luajit \
	LUA_LIB=$(pkg-config --libs luajit)

mkdir -p %{buildroot}%{lua_archdir}
mv mpack.so.lua %{buildroot}%{lua_archdir}/mpack.so

%files
%doc LICENSE-MIT README.md
%dir %{lua_archdir}
%{lua_archdir}/*

%files -n luajit-mpack
%doc LICENSE-MIT README.md
%{luajit_archdir}/*
