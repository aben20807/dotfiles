let macvim_skip_colorscheme=1
function! s:InstallVimPlug()
    if empty(glob('~/.vim/autoload/plug.vim'))
      silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
        \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
      autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
    endif
endfunction

call s:InstallVimPlug()

call plug#begin('~/.vim/plugged')
" Theme
Plug 'chriskempson/base16-vim'

Plug 'andymass/vim-matchup'
Plug 'aben20807/vim-runner'
Plug 'aben20807/vim-commenter'
let g:commenter_n_key = "<C-j>"
let g:commenter_i_key = "<C-j>"
let g:commenter_v_key = "<C-j>"

Plug 'Exafunction/codeium.vim', { 'branch': 'main' }
let g:codeium_no_map_tab = 1
imap <script><silent><nowait><expr> <C-g> codeium#Accept()
imap <C-t>   <Cmd>call codeium#CycleCompletions(1)<CR>
imap <C-b>   <Cmd>call codeium#CycleCompletions(-1)<CR>
imap <C-x>   <Cmd>call codeium#Clear()<CR>

" For git commit
Plug 'rhysd/committia.vim'
let g:committia_hooks = {}
function! g:committia_hooks.edit_open(info)
    " Additional settings
    setlocal spell

    " If no commit message, start with insert mode
    if a:info.vcs ==# 'git' && getline(1) ==# ''
        startinsert
    endif

    " Scroll the diff window from insert mode
    " Map <C-n> and <C-p>
    imap <buffer><C-n> <Plug>(committia-scroll-diff-down-half)
    imap <buffer><C-p> <Plug>(committia-scroll-diff-up-half)
endfunction

call plug#end()

" let cursor in the middle of screen when entering vim
autocmd VimEnter * :exec "normal! \zz"

" return to last edit position when opening files
autocmd BufReadPost *
            \ if line("'\"") > 0 && line("'\"") <= line('$') |
            \   exe "normal! g`\"" |
            \ endif

" =============================================================================
" # Color
" =============================================================================
set t_Co=256
set termguicolors
set background=dark
let base16colorspace=256
set rtp+=~/.config/nvim/plugged/base16-vim/
colorscheme base16-gruvbox-dark-hard
syntax on

" =============================================================================
" # Editor settings
" =============================================================================
filetype off
filetype plugin indent on
set updatetime=300
set noesckeys
set autoindent
set notimeout
set nottimeout
set encoding=utf-8
set scrolloff=2
set noshowmode
set hidden
set nowrap
set nojoinspaces
" Always draw sign column. Prevent buffer moving when adding/deleting sign.
set signcolumn=yes
set laststatus=2
set statusline=%F%r%h%w%=\ [%Y]\ [%04l,%04v]\ [%p%%]\ [%L]

" let new page occurred at right or below
set splitright
set splitbelow

" Proper search
set incsearch
set ignorecase
set smartcase
set gdefault

" let italic enable
" Ref: https://askubuntu.com/a/514524
set t_ZH=[3m
set t_ZR=[23m
" Weird char 001B[>4;m 001B[>4;2m
" Ref: https://stackoverflow.com/a/62150215/6734174
let &t_TI = ""
let &t_TE = ""
" Show those hidden characters
set listchars=nbsp:¬,extends:»,precedes:«,trail:•

" let cursor in the middle of screen when entering vim
autocmd VimEnter * :exec "normal! \zz"

" return to last edit position when opening files
autocmd BufReadPost *
            \ if line("'\"") > 0 && line("'\"") <= line('$') |
            \   exe "normal! g`\"" |
            \ endif

" let history record=1000
set history=1000
" let undo history not be clear after changing buffer
" Ref: https://stackoverflow.com/a/22676189/6734174
let vimDir = '$HOME/.config/nvim/'
let &runtimepath .= ',' . vimDir

" Keep undo history across sessions by storing it in a file
if has('persistent_undo')
    let myUndoDir = expand(vimDir . '/undodir')
    " Create dirs
    silent! call mkdir(myUndoDir, 'p')
    let &undodir = myUndoDir
    set undofile
    set undolevels=1000
    set undoreload=10000
endif
" --- backup ---
" nobackup + writebackup = backup current file, deleted afterwards (default)
" no backup
set nobackup
" write into backup file
set writebackup
" not use swap file
set noswapfile

" not auto comment when changing line
" Ref: http://vim.wikia.com/wiki/Disable_automatic_comment_insertion
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" --- tab ---
set tabstop=4
set softtabstop=4
set expandtab
set shiftwidth=4

" Allow the cursor to move just past the end of the line
set virtualedit=onemore

" show detailed mode
set showmode

" let labels not auto indent
set cinoptions+=L0

" auto change directory
"set autochdir

" auto update if file changed in other way
set autoread
autocmd FileChangedShellPost *
            \ redraw | echohl WarningMsg | echo "File changed on disk. Buffer reloaded." | echohl None
function! Fresh(arg) abort
    " Ref: https://vi.stackexchange.com/a/14317
    if !bufexists("[Command Line]") | checktime | endif
endfunction
let timer = timer_start(5000,  'Fresh', {'repeat': -1})

" igonre file
set wildignore+=*.o,*.obj,*.pyc
let mapleader = "\<Space>"
set mouse=a

" =============================================================================
" # Key map
" =============================================================================
nnoremap q: :q
nnoremap <F1> <NOP>
vnoremap <F1> <NOP>

nnoremap <expr> k (v:count == 0 ? 'gk' : 'k')
nnoremap <expr> j (v:count == 0 ? 'gj' : 'j')
inoremap <silent> <UP> <C-o>gk
inoremap <silent> <DOWN> <C-o>gj

" let <F> key not type in insert mode
" inoremap <F2>  <ESC><F2><CR>i
imap <F2>  <ESC><F2>li
imap <F3>  <ESC><F3>li
imap <F4>  <ESC><F4>li
imap <F5>  <ESC><F5>
imap <F6>  <ESC><F6>li
imap <F8>  <ESC><F8>li
imap <F9>  <ESC><F9>li
imap <F10> <ESC><F10>li
imap <F11> <ESC><F11>li
imap <F12> <ESC><F12>li

" background vim
inoremap <C-z> <C-o><C-z>

" tab indent
vmap <TAB> >gv
vmap <S-TAB> <gv

" indent
nmap < <<
nmap > >>
vnoremap < <gv
vnoremap > >gv

" search select text by pressing // in visual mode
" Ref: http://vim.wikia.com/wiki/Search_for_visually_selected_text
vnoremap // y/\V<C-r>=escape(@",'/\')<CR><CR>
vnoremap <C-f> y/\V<C-r>=escape(@",'/\')<CR><CR>

" Not overwrite paste buffer after pasting
" Ref: https://stackoverflow.com/a/290723/6734174
function! RestoreRegister()
      let @" = s:restore_reg
        return ''
endfunction

function! s:Repl()
        let s:restore_reg = @"
            return "p@=RestoreRegister()\<CR>"
endfunction

" NB: this supports "rp that replaces the selection by the contents of @r
vnoremap <silent> <expr> p <SID>Repl()

" show line numbers, use <F2> to switch
nnoremap <F2> :set norelativenumber!<CR>:set nonumber!<CR>
:set number
:set relativenumber
