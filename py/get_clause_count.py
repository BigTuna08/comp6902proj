'''
Assumes
- both graphs have equal number of nodes
- m0 = m was used when creating graphs
'''

def get_type3_clause_count(n, k, m_g_gen, m_h_gen):
    m_g = m_g_gen + n*m_g_gen - m_g_gen **2 # total edges in g (assuming m0 = m)
    m_h = m_h_gen + n*m_h_gen - m_h_gen **2 # total edges in h (assuming m0 = m)

    if m_g_gen < 3: # no inital cycle
        m_g -= 1
    if m_h_gen < 3:
        m_h -= 1

    return k*(k-1)/2*( n*(n-1)/2*(m_g + m_h) - 2*m_g*m_h )

def get_type2_clause_count(n, k):
    return (k-1)*(k)*n

def get_type1_clause_count(k):
    return 2*k

def get_clause_count(n, k, m_g, m_h):
    print("computed, with ", n, k, m_g, m_h)
    print(get_type1_clause_count(k), "type 1")
    print(get_type2_clause_count(n,k), "type 2")
    print(get_type3_clause_count(n, k, m_g, m_h), "type 3")
    print("\n counted ")
    return get_type1_clause_count(k) + get_type2_clause_count(n,k) + get_type3_clause_count(n, k, m_g, m_h)
