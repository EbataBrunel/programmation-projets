package busness.ecommerce.controller;

import busness.ecommerce.dto.AttributeResponseDto;
import busness.ecommerce.dto.AttributeValueRequestDto;
import busness.ecommerce.dto.AttributeValueResponseDto;
import busness.ecommerce.services.AttributeValueService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/attribute-values")
@RequiredArgsConstructor
public class AttributeValueRestController {
    private final AttributeValueService service;

    @PostMapping
    public AttributeValueResponseDto create(
            @RequestBody AttributeValueRequestDto dto) {
        return service.create(dto);
    }

    @GetMapping
    public List<AttributeValueResponseDto> all() {
        return service.getAll();
    }

    // Récupérer une valeur d'attribut par id
    @GetMapping("/{id}")
    public ResponseEntity<AttributeValueResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(service.getAttributeValueById(id));
    }

    @GetMapping("/get/{id}")
    public List<AttributeValueResponseDto> getByAttribute(
            @PathVariable Long id) {
        return service.findByAttribute(id);
    }

    // Modifier une valeur attribut
    @PutMapping("/{id}")
    public ResponseEntity<AttributeValueResponseDto> update(
            @PathVariable Long id,
            @RequestBody AttributeValueRequestDto dto
    ) {
        return ResponseEntity.ok(service.updateAttributeValue(id, dto));
    }

    // Supprimer une valeur attribut
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        service.deleteAttributeValue(id);
        return ResponseEntity.noContent().build();
    }
}
