"""
Supabase client initialization for Logos Pulse.
Provides cached clients for both anon (user-scoped) and admin (service role) access.
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase_client() -> Client:
    """Get a Supabase client using the anon key (respects RLS)."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)


@st.cache_resource
def get_admin_client() -> Client:
    """Get a Supabase client using the service role key (bypasses RLS).
    Use ONLY for admin operations: account creation, seeding, migrations.
    """
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]
    return create_client(url, key)