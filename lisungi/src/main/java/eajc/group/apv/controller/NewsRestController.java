package eajc.group.apv.controller;

import eajc.group.apv.dto.NewsRequestDto;
import eajc.group.apv.dto.NewsResponseDto;
import eajc.group.apv.services.NewsService;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/news")
public class NewsRestController {
    private final NewsService newsService;

    public NewsRestController(NewsService newsService) {
        this.newsService = newsService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<NewsResponseDto> create(
            @RequestPart("data") NewsRequestDto dto,
            @RequestParam(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException {
        return ResponseEntity.ok(newsService.createNews(dto, photoFile));
    }

    // Récupérer toutes les actualités
    @GetMapping
    public ResponseEntity<List<NewsResponseDto>> getAll() {
        return ResponseEntity.ok(newsService.getAllNews());
    }

    // Récupérer une actualité par id
    @GetMapping("/{publicId}")
    public ResponseEntity<NewsResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(newsService.getNewsByPublicId(publicId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier une actualité
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<NewsResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") NewsRequestDto dto,
            @RequestPart(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException {
        return ResponseEntity.ok(newsService.updateNews(publicId, dto, photoFile));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer une actualité
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        newsService.deleteNews(publicId);
        return ResponseEntity.noContent().build();
    }
}
