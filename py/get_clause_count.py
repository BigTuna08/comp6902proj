'''
Assumes
- both graphs have equal number of nodes
- m0 = m was used when creating graphs
'''

def get_type3_clause_count(n, k, m_g, m_h):
    m_g = m_g + n*m_g - m_g **2 # total edges in g (assuming m0 = m)
    m_h = m_h + n*m_h - m_h **2 # total edges in h (assuming m0 = m)
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
