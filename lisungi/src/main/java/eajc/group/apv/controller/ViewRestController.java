package eajc.group.apv.controller;

import eajc.group.apv.dto.ViewRequestDto;
import eajc.group.apv.dto.ViewResponseDto;
import eajc.group.apv.services.CustomUserDetails;
import eajc.group.apv.services.ViewService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/views")
public class ViewRestController {
    private final ViewService viewService;

    public ViewRestController(ViewService viewService) {
        this.viewService = viewService;
    }

    @PostMapping("/create-missing")
    public ResponseEntity<Integer> createMissingViews(
            Authentication authentication
    ){
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Administrateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();
        return ResponseEntity.ok(viewService.createMissingViews(user.getUser().getId()));
    }

    // Récupérer toutes les vues
    @GetMapping("/admin")
    public ResponseEntity<List<ViewResponseDto>> getViewdByAdminIdAndStatusFalse(
            Authentication authentication
    ){
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Administrateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();
        return ResponseEntity.ok(viewService.getViewdByAdminIdAndStatusFalse(user.getUser().getId()));
    }

    // Récupérer un évènement par id
    @GetMapping("/{publicId}")
    public ResponseEntity<ViewResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(viewService.getView(publicId));
    }


    // Modifier le status de vue
    @PatchMapping("/update-status")
    public ResponseEntity<?> markAllViewsAsViewed(
            Authentication authentication
    ) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Administrateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        int updated = viewService.markAllViewsAsViewed(
                user.getUser().getId()
        );

        return ResponseEntity.ok(updated);
    }

    // Compter les utilisateur qui n'ont pas de vue avec l'admin
    @GetMapping("/count-view")
    public ResponseEntity<?> getCountUsersNotViewWithAdmin(
            Authentication authentication
    ){
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Administrateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();
        return ResponseEntity.ok(viewService.countUsersNotViewWithAdmin(user.getUser().getId()));
    }

}
