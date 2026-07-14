package busness.ecommerce.controller;

import busness.ecommerce.dto.ProductAttributeRequestDto;
import busness.ecommerce.dto.ProductAttributeResponseDto;
import busness.ecommerce.services.ProductAttributeService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/product-attributes")
@RequiredArgsConstructor
public class ProductAttributeController {

    private final ProductAttributeService service;

    @PostMapping
    public ProductAttributeResponseDto create(
            @RequestBody ProductAttributeRequestDto dto) {

        return service.create(dto);
    }

    @GetMapping("/variant/{variantId}")
    public List<ProductAttributeResponseDto> getByVariant(
            @PathVariable Long variantId) {

        return service.getByVariant(variantId);
    }
}

