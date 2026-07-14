package busness.ecommerce.controller;

import busness.ecommerce.dto.AttributeRequestDto;
import busness.ecommerce.dto.AttributeResponseDto;
import busness.ecommerce.dto.CategoryResponseDto;
import busness.ecommerce.services.AttributeService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/attributes")
@RequiredArgsConstructor
public class AttributeRestController {

    private final AttributeService service;

    @PostMapping
    public AttributeResponseDto create(@RequestBody AttributeRequestDto request) {
        return service.create(request);
    }

    @GetMapping
    public List<AttributeResponseDto> all() {
        return service.getAll();

    }

    // Récupérer un attribut par id
    @GetMapping("/{id}")
    public ResponseEntity<AttributeResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(service.getAttributeById(id));
    }

    // Modifier un attribut
    @PutMapping("/{id}")
    public ResponseEntity<AttributeResponseDto> update(
            @PathVariable Long id,
            @RequestBody AttributeRequestDto request
    ) {
        return ResponseEntity.ok(service.updateAttribute(id, request));
    }

    // Supprimer un attribut
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        service.deleteAttribute(id);
        return ResponseEntity.noContent().build();
    }
}

