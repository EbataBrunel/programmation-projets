package eajc.group.apv.services;

import eajc.group.apv.dto.NewsRequestDto;
import eajc.group.apv.dto.NewsResponseDto;
import eajc.group.apv.entity.News;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.NewsMapper;
import eajc.group.apv.repository.NewsRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;

@Service
public class NewsServiceImpl implements NewsService{

    private final NewsRepository newsRepository;
    private final NewsMapper newsMapper;
    private final FileStorageService fileStorageService;

    public NewsServiceImpl(NewsRepository newsRepository, NewsMapper newsMapper, FileStorageService fileStorageService) {
        this.newsRepository = newsRepository;
        this.newsMapper = newsMapper;
        this.fileStorageService = fileStorageService;
    }


    @Override
    public NewsResponseDto createNews(NewsRequestDto dto, MultipartFile photoFile) throws IOException {
        if (dto.getTitle() == null || dto.getTitle().trim().isEmpty()) {
            throw new BadRequestException("Le titre est obligatoire.");
        }

        if (dto.getContent() == null || dto.getContent().trim().isEmpty()) {
            throw new BadRequestException("Le contenu est obligatoire.");
        }

        if (newsRepository.existsByTitleIgnoreCase(dto.getTitle().trim())) {
            throw new BadRequestException("Ce titre existe déjà.");
        }

        String fileName = fileStorageService.saveFile(photoFile);

        News news = newsMapper.toEntity(dto, fileName);
        News newsSave = newsRepository.save(news);
        return newsMapper.toDto(newsSave);
    }

    @Override
    public List<NewsResponseDto> getAllNews() {
        return newsRepository.findAll()
                .stream()
                .map(newsMapper::toDto)
                .toList();
    }

    @Override
    public NewsResponseDto getNewsByPublicId(UUID publicId) {
        News news = newsRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Actualité introuvable"));
        return newsMapper.toDto(news);
    }

    @Override
    public NewsResponseDto updateNews(
            UUID publicId,
            NewsRequestDto dto,
            MultipartFile photoFile) throws IOException {

        if (dto.getTitle() == null || dto.getTitle().trim().isEmpty()) {
            throw new BadRequestException("Le titre est obligatoire.");
        }

        if (dto.getContent() == null || dto.getContent().trim().isEmpty()) {
            throw new BadRequestException("Le contenu est obligatoire.");
        }

        if (newsRepository.existsByTitleIgnoreCaseAndPublicIdNot(
                dto.getTitle().trim(), publicId)) {

            throw new BadRequestException("Ce titre existe déjà.");
        }

        News news = newsRepository.findByPublicId(publicId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Actualité introuvable"));

        news.setTitle(dto.getTitle().trim());
        news.setContent(dto.getContent());

        if (photoFile != null && !photoFile.isEmpty()) {

            // Garder l'ancienne URL
            String oldPhoto = news.getPhoto();

            // 1. Upload de la nouvelle photo
            String newPhoto = fileStorageService.saveFile(photoFile);

            // 2. Enregistrer la nouvelle URL
            news.setPhoto(newPhoto);

            // 3. Supprimer l'ancienne photo de Cloudinary
            if (oldPhoto != null
                    && !oldPhoto.isBlank()
                    && oldPhoto.startsWith("http")) {

                try {
                    fileStorageService.deleteFile(oldPhoto);
                } catch (Exception e) {
                    System.err.println(
                            "Impossible de supprimer l'ancienne image Cloudinary : "
                                    + e.getMessage()
                    );
                }
            }
        }

        News savedNews = newsRepository.save(news);

        return newsMapper.toDto(savedNews);
    }

    @Override
    public void deleteNews(UUID publicId) {
        News news = newsRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Actualité introuvable"));

        if (news.getPhoto() != null && !news.getPhoto().isBlank()) {
            fileStorageService.deleteFile(news.getPhoto());
        }

        newsRepository.delete(news);
    }
}
