%define lua_version %(lua -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define lua_archdir %{_libdir}/lua/%{lua_version}
%global lua_libdir %{_libdir}/lua/%{lua_version}

%define luajit_version %(luajit -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define luajit_archdir %{_libdir}/lua/%{luajit_version}
%global luajit_libdir %{_libdir}/lua/%{luajit_version}

# Bootstrap with --without lua (lua-mpack:-lua) to keep only luajit-mpack.
%bcond_without lua
%bcond_without luajit

Name:           lua-mpack
Version:        1.0.12
Release:        1
Summary:        Implementation of MessagePack for Lua
License:        MIT
Group:          Development/Other
Url:            https://github.com/libmpack/libmpack-lua
Source:         https://github.com/libmpack/libmpack-lua/archive/refs/tags/%{version}.tar.gz
Source1:	https://github.com/tarruda/libmpack/archive/1.0.5.tar.gz
BuildRequires:	make
BuildRequires:  libtool
%if %{with lua}
BuildRequires:  lua-devel
Requires:       lua
%endif
%if %{with luajit}
BuildRequires:	luajit
BuildRequires:	pkgconfig(luajit)
%endif

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
%if %{with lua}
# Makefile links with $(LIBS), not LUA_LIB.
%make_build %{?_smp_mflags} \
	USE_SYSTEM_LUA=yes \
	CC="%{__cc}" \
	CFLAGS="%{optflags}" \
	LUA_VERSION_MAJ_MIN=%{lua_version} \
	LUA_INCLUDE="$(pkg-config --cflags lua)" \
	LIBS="$(pkg-config --libs lua)" \
	FETCH=cat \
	MPACK_URL="%{S:1}"
mv mpack.so mpack.so.lua
%if %{with luajit}
%make_build clean
%endif
%endif

%if %{with luajit}
%make_build %{?_smp_mflags} \
	USE_SYSTEM_LUA=yes \
	CC="%{__cc}" \
	CFLAGS="%{optflags}" \
	LUA_VERSION_MAJ_MIN=%{luajit_version} \
	LUA_IMPL=luajit \
	LUA_INCLUDE="$(pkg-config --cflags luajit)" \
	LIBS="$(pkg-config --libs luajit)" \
	FETCH=cat \
	MPACK_URL="%{S:1}"
%endif

%install
%if %{with luajit}
%make_install \
	USE_SYSTEM_LUA=yes \
	LUA_CMOD_INSTALLDIR=%{luajit_libdir} \
	LUA_VERSION_MAJ_MIN=%{luajit_version} \
	LUA_IMPL=luajit \
	LIBS="$(pkg-config --libs luajit)"
%endif

%if %{with lua}
mkdir -p %{buildroot}%{lua_archdir}
mv mpack.so.lua %{buildroot}%{lua_archdir}/mpack.so
%endif

%if %{with lua}
%files
%doc LICENSE-MIT README.md
%dir %{lua_archdir}
%{lua_archdir}/*
%endif

%if %{with luajit}
%files -n luajit-mpack
%doc LICENSE-MIT README.md
%{luajit_archdir}/*
%endif
