using System.Collections.Generic;
namespace AceriaApp.Api.Repository;

public class CatalogoRepositorios
{
    public static List<Repositorio> RepositoriosPorDefecto()
    {
        return new List<Repositorio>
        {
            new() { Nombre = "IOrdenRepositorio", Entidad = "Orden", NumeroDeMetodos = 5, TieneReglasDeNegocio = false, GestionaTransacciones = false },
            new() { Nombre = "IInventarioRepositorio", Entidad = "Material", NumeroDeMetodos = 5, TieneReglasDeNegocio = false, GestionaTransacciones = false },
            new() { Nombre = "IClienteRepositorio", Entidad = "Cliente", NumeroDeMetodos = 4, TieneReglasDeNegocio = false, GestionaTransacciones = false }
        };
    }
}
