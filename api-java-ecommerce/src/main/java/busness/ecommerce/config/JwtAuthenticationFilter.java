package busness.ecommerce.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtUtils jwtUtils;

    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        String path = request.getServletPath();

        // ROUTES PUBLIQUES → ON SKIPPE LE FILTRE JWT
        if (
                path.startsWith("/api/v1/auth/login") ||
                        path.startsWith("/api/v1/auth/register") ||
                        path.startsWith("/api/v1/auth/forgot-password") ||
                        path.startsWith("/api/v1/auth/reset-password") ||
                        path.startsWith("/api/v1/categories") ||
                        path.startsWith("/api/v1/subcategories") ||
                        path.startsWith("/api/v1/attributes") ||
                        path.startsWith("/api/v1/attribute-values") ||
                        path.startsWith("/api/v1/product-variants") ||
                        path.startsWith("/api/v1/contacts") ||
                        path.startsWith("/api/v1/settings") ||
                        path.startsWith("/api/v1/questions") ||
                        path.startsWith("/api/v1/answers") ||
                        path.startsWith("/api/v1/brands") ||
                        path.startsWith("/webhook/stripe") ||
                        path.startsWith("/uploads/**")
        ) {
            filterChain.doFilter(request, response);
            return;
        }

        final String authHeader = request.getHeader("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        String token = authHeader.substring(7);
        String username = jwtUtils.extractUsername(token);

        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);

            if (jwtUtils.isTokenValid(token, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                        new UsernamePasswordAuthenticationToken(
                                userDetails,
                                null,
                                userDetails.getAuthorities()
                        );

                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        filterChain.doFilter(request, response);
    }
}
