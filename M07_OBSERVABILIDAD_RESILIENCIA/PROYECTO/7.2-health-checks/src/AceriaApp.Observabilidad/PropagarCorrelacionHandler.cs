using Microsoft.AspNetCore.Http;
namespace AceriaApp.Observabilidad;
public sealed class PropagarCorrelacionHandler(IHttpContextAccessor accessor) : DelegatingHandler
{
    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
    {
        request.Headers.Remove(ContextoCorrelacion.Cabecera);
        var id = accessor.HttpContext is { } context ? ContextoCorrelacion.Obtener(context) : "";
        if (id.Length > 0) request.Headers.Add(ContextoCorrelacion.Cabecera, id);
        return base.SendAsync(request, ct);
    }
}
