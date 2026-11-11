namespace AceriaApp.Produccion.Aplicacion;
public sealed class ConflictoProduccionException() : Exception("La orden cambió desde su lectura; vuelve a consultarla.");
