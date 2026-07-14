package busness.ecommerce.controller;


import busness.ecommerce.dto.FrequentlyQuestionRequestDto;
import busness.ecommerce.dto.FrequentlyQuestionResponseDto;
import busness.ecommerce.services.FrequentlyQuestionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/questions")

public class FrequentlyQuestionRestController {
    private final FrequentlyQuestionService frequentlyQuestionService;

    @PostMapping
    public FrequentlyQuestionResponseDto create(@RequestBody FrequentlyQuestionRequestDto request) {
        return frequentlyQuestionService.create(request);
    }

    @GetMapping
    public List<FrequentlyQuestionResponseDto> all() {
        return frequentlyQuestionService.getAll();

    }

    // Récupérer une question par id
    @GetMapping("/{id}")
    public ResponseEntity<FrequentlyQuestionResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(frequentlyQuestionService.getFrequentlyQuestionById(id));
    }

    // Modifier une question
    @PutMapping("/{id}")
    public ResponseEntity<FrequentlyQuestionResponseDto> update(
            @PathVariable Long id,
            @RequestBody FrequentlyQuestionRequestDto request
    ) {
        return ResponseEntity.ok(frequentlyQuestionService.updateFrequentlyQuestion(id, request));
    }

    // Supprimer une question
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        frequentlyQuestionService.deleteFrequentlyQuestion(id);
        return ResponseEntity.noContent().build();
    }
}
