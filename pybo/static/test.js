document.querySelectorAll('.delete').forEach(element => {
    element.addEventListener('click', e => {
        if(confirm("정말로 삭제하시겠습니까?")) {
            // this는 element(클릭된 요소)를 가리킴
            // this.dataset.uri -> html요소의 data-uri 속성
            location.href = element.dataset.uri;
            // 삭제 확인 후 바로 data-uri에 지정된 url로 이동
        };
    });
});

document.querySelectorAll('.recommend').forEach(element => {
    element.addEventListener('click', e => {
        if(confirm("정말로 추천하시겠습니까?")) {
            location.href = element.dataset.uri;
            };
    });
});

const page_elements = document.querySelectorAll(".page-link");
page_elements.forEach(element => {
   element.addEventListener('click', (e) => {
   // a tag의 data-page 속성값을 읽어 searchForm의 page 필드에 설정 -> searchForm 요청
    document.querySelector('#page').value = element.dataset.page;
    document.querySelector('#searchForm').submit();
   });
});

const btn_search = document.querySelector("#btn_search");
btn_search.addEventListener('click', (e) => {
    // 검색창에 입력된 내용을 읽어 searchForm의 kw 필드에 설정 -> searchForm 요청
    document.querySelector('#kw').value = document.querySelector('#search_kw').value;
    document.querySelector('#page').value = 1; // 검색 시 1페이지부터 조회
    document.querySelector('#searchForm').submit();
});