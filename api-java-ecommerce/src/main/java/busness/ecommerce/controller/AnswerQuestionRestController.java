package busness.ecommerce.controller;


import busness.ecommerce.dto.AnswerQuestionRequestDto;
import busness.ecommerce.dto.AnswerQuestionResponseDto;
import busness.ecommerce.services.AnswerQuestionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/answers")
public class AnswerQuestionRestController {
    private final AnswerQuestionService answerQuestionService;

    // Ajouter une réponse
    @PostMapping
    public ResponseEntity<AnswerQuestionResponseDto> create(
            @RequestBody AnswerQuestionRequestDto dto
    ){
        return ResponseEntity.ok(answerQuestionService.createAnswerQuestion(dto));
    }

    // Récupérer toutes les réponses
    @GetMapping
    public ResponseEntity<List<AnswerQuestionResponseDto>> getAll() {
        return ResponseEntity.ok(answerQuestionService.getAllAnswerQuestions());
    }

    // Récupérer une réponse par id
    @GetMapping("/{id}")
    public ResponseEntity<AnswerQuestionResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(answerQuestionService.getAnswerQuestionById(id));
    }

    // Modifier une réponse
    @PutMapping("/{id}")
    public ResponseEntity<AnswerQuestionResponseDto> update(
            @PathVariable Long id,
            @RequestBody AnswerQuestionRequestDto dto
    ) {
        return ResponseEntity.ok(answerQuestionService.updateAnswerQuestion(id, dto));
    }

    // Supprimer une réponse
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        answerQuestionService.deleteAnswerQuestion(id);
        return ResponseEntity.noContent().build();
    }
}
