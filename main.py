from ManipuladorArquivo import ManipuladorArquivo
from simulated_annealing_p_medians import SimulatedAnnealing

if __name__ == "__main__":
    ma = ManipuladorArquivo("pmed40.txt.table.p56.B")
    distancias = ma.obter_distancias_facilidades()
    n = ma.obter_n_clients()
    I = ma.obter_clientes()
    m = ma.obter_m_facilities()
    J = ma.obter_facilidades()
    p = ma.obter_p_desired_facilities()
    sa = SimulatedAnnealing(n, I, m, J, p, distancias)
    sa.executa()
